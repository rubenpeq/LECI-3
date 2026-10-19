// Helper file for SIC Lab on Symmetric Cryptography

#include <stdint.h>
#include <assert.h>

#include "aes.h"
#include "padding.h"

// Adds PKCS#7 padding and returns the new plaintext length

int add_padding(uint8_t *plain, const int plain_size)
{
    assert(plain != 0);

    // Determine padding length (1 to 16 bytes)
    uint8_t pad_val = AES128_BLOCK_SIZE - (plain_size % AES128_BLOCK_SIZE);

    // Append pad_val repeatedly
    for (int i = 0; i < pad_val; i++)
    {
        plain[plain_size + i] = pad_val;
    }

    return plain_size + pad_val;
}

/*
 * Checks PKCS#7 padding and returns the original plaintext length (w/o padding)
 * If an error is found in the padding, it returns -1.
 */

int rm_padding(uint8_t *padded, const int full_size)
{
    assert(padded != 0);

    // Valid block cipher output must be non-zero and a multiple of 16
    if (full_size <= 0 || (full_size % AES128_BLOCK_SIZE) != 0)
    {
        return -1;
    }

    // Read value of last byte
    uint8_t pad_val = padded[full_size - 1];

    // PKCS#7 padding value must be between 1 and AES128_BLOCK_SIZE (16)
    if (pad_val == 0 || pad_val > AES128_BLOCK_SIZE)
    {
        return -1;
    }

    // Verify all pad_val bytes match expected padding value
    for (int i = 0; i < pad_val; i++)
    {
        if (padded[full_size - 1 - i] != pad_val)
        {
            return -1; // Padding integrity check failed
        }
    }

    return full_size - pad_val;
}
