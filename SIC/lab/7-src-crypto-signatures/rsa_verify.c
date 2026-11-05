#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/rsa.h>

#include "digest_file.h"

static EVP_PKEY *
load_public_key(const char *path)
{
    FILE *file = fopen(path, "r");
    EVP_PKEY *key;
    if (file == NULL)
    {
        fprintf(stderr, "Could not open public key \"%s\"\n", path);
        return NULL;
    }
    key = PEM_read_PUBKEY(file, NULL, NULL, NULL);
    fclose(file);
    if (key == NULL || EVP_PKEY_is_a(key, "RSA") == 0)
    {
        fprintf(stderr, "Could not load an RSA public key from \"%s\"\n", path);
        EVP_PKEY_free(key);
        return NULL;
    }
    return key;
}

static int
read_signature(const char *path, unsigned char **signature, size_t *signature_len)
{
    FILE *file = strcmp(path, "-") == 0 ? stdin : fopen(path, "rb");
    size_t len = 0, capacity = 4096;
    unsigned char *buffer;
    if (file == NULL)
    {
        fprintf(stderr, "Could not open signature file \"%s\"\n", path);
        return 0;
    }
    buffer = malloc(capacity);
    if (buffer == NULL)
        goto fail;
    for (;;)
    {
        if (len == capacity)
        {
            size_t new_capacity = capacity * 2;
            unsigned char *grown = realloc(buffer, new_capacity);
            if (grown == NULL)
                goto fail;
            buffer = grown;
            capacity = new_capacity;
        }
        size_t n = fread(buffer + len, 1, capacity - len, file);
        len += n;
        if (n == 0)
        {
            if (ferror(file))
                goto fail;
            break;
        }
    }
    if (file != stdin)
        fclose(file);
    *signature = buffer;
    *signature_len = len;
    return len > 0;
fail:
    fprintf(stderr, "Could not read signature data\n");
    free(buffer);
    if (file != stdin)
        fclose(file);
    return 0;
}

int main(int argc, char **argv)
{
    EVP_PKEY *key = NULL;
    EVP_MD *md = NULL;
    EVP_PKEY_CTX *ctx = NULL;
    unsigned char *digest = NULL, *signature = NULL;
    size_t signature_len = 0;
    int fd = -1, padding, result = 2;

    if (argc != 5 && argc != 6)
    {
        fprintf(stderr, "Usage: %s public_key_PEM_file padding digest_function signed_file [signature_file|-]\n", argv[0]);
        fprintf(stderr, "\tpadding: PKCS1 or PSS; signature defaults to stdin\n");
        return 2;
    }
    if (strcmp(argv[2], "PKCS1") == 0)
        padding = RSA_PKCS1_PADDING;
    else if (strcmp(argv[2], "PSS") == 0)
        padding = RSA_PKCS1_PSS_PADDING;
    else
    {
        fprintf(stderr, "Invalid padding \"%s\"\n", argv[2]);
        return 2;
    }
    md = EVP_MD_fetch(NULL, argv[3], NULL);
    if (md == NULL)
    {
        fprintf(stderr, "Unknown digest function \"%s\"\n", argv[3]);
        goto cleanup;
    }
    key = load_public_key(argv[1]);
    if (key == NULL)
        goto cleanup;
    fd = strcmp(argv[4], "-") == 0 ? STDIN_FILENO : open(argv[4], O_RDONLY);
    if (fd < 0)
    {
        fprintf(stderr, "Could not open signed file \"%s\"\n", argv[4]);
        goto cleanup;
    }
    digest = malloc(EVP_MD_get_size(md));
    if (digest == NULL || digest_file(fd, md, digest) == 0)
    {
        fprintf(stderr, "Could not compute digest of signed file\n");
        goto cleanup;
    }
    close(fd);
    fd = -1;
    if (!read_signature(argc == 6 ? argv[5] : "-", &signature, &signature_len))
        goto cleanup;

    ctx = EVP_PKEY_CTX_new_from_pkey(NULL, key, NULL);
    if (ctx == NULL || EVP_PKEY_verify_init(ctx) <= 0 ||
        EVP_PKEY_CTX_set_signature_md(ctx, md) <= 0 ||
        EVP_PKEY_CTX_set_rsa_padding(ctx, padding) <= 0)
    {
        fprintf(stderr, "Could not initialize RSA verification\n");
        goto cleanup;
    }
    if (padding == RSA_PKCS1_PSS_PADDING &&
        (EVP_PKEY_CTX_set_rsa_mgf1_md(ctx, md) <= 0 ||
         EVP_PKEY_CTX_set_rsa_pss_saltlen(ctx, RSA_PSS_SALTLEN_DIGEST) <= 0))
    {
        fprintf(stderr, "Could not configure RSA-PSS verification\n");
        goto cleanup;
    }

    int verified = EVP_PKEY_verify(ctx, signature, signature_len,
                                   digest, EVP_MD_get_size(md));
    if (verified == 1)
    {
        puts("Signature is valid");
        result = 0;
    }
    else if (verified == 0)
    {
        puts("Signature is invalid");
        result = 1;
    }
    else
    {
        fprintf(stderr, "Signature verification failed (invalid parameters or signature format)\n");
        result = 1;
    }

cleanup:
    if (fd >= 0)
        close(fd);
    free(digest);
    free(signature);
    EVP_PKEY_CTX_free(ctx);
    EVP_PKEY_free(key);
    EVP_MD_free(md);
    return result;
}
