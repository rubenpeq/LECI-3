#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>

#include "linked-list.h"

/*******************************************************/

SllNode *sllDestroy(SllNode *list)
{
    return list;
}

/*******************************************************/

void sllPrint(SllNode *list, FILE *fout)
{
    while (list != NULL)
    {
        fprintf(fout, "%u, %s\n", list->reg.nmec, list->reg.name);
        list = list->next;
    }
}

/*******************************************************/

SllNode *sllInsert(SllNode *list, uint32_t nmec, const char *name)
{
    assert(name != NULL && name[0] != '\0');
    assert(!sllExists(list, nmec));

    // Create new node
    SllNode *newNode = (SllNode *)malloc(sizeof(SllNode));

    newNode->next = NULL;
    newNode->reg.nmec = nmec;
    newNode->reg.name = strdup(name);

    // Add new node to the list

    if (list == NULL)
        return newNode;

    if (nmec < list->reg.nmec)
    {
        newNode->next = list;
        return newNode;
    }

    SllNode *cur = list;
    while (cur->next != NULL && cur->next->reg.nmec < nmec)
        cur = cur->next;

    newNode->next = cur->next;
    cur->next = newNode;

    return list;
}

/*******************************************************/

bool sllExists(SllNode *list, uint32_t nmec)
{
    SllNode *cur = list;

    // check all list for nmec
    while (cur != NULL)
    {
        if (cur->reg.nmec == nmec)
            return true;
        cur = cur->next;
    }

    return false;
}

/*******************************************************/

SllNode *sllRemove(SllNode *list, uint32_t nmec)
{
    assert(list != NULL);
    assert(sllExists(list, nmec));

    return list;
}

/*******************************************************/

const char *sllGetName(SllNode *list, uint32_t nmec)
{
    assert(list != NULL);
    assert(sllExists(list, nmec));

    return NULL;
}

/*******************************************************/

SllNode *sllLoad(SllNode *list, FILE *fin, bool *ok)
{
    assert(fin != NULL);

    if (ok != NULL)
        *ok = false; // load failure

    return NULL;
}

/*******************************************************/
