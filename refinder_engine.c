#include "refinder_engine.h"
#include "kmp.c"
#include <stdlib.h>
#include <string.h>
#include <ftw.h>
#include <sys/stat.h>

char search_pattern[261] = {'\0'};
pfile file_list = NULL;

static int addNode(pfile *table, const char *file_name, char file_type)
{
	pfile nextNode = (pfile)malloc(sizeof(file));
	memset(nextNode->file_name, '\0', sizeof(nextNode->file_name));
	nextNode->file_type = file_type;
	strcpy(nextNode->file_name, file_name);
	nextNode->next = *table;
	*table = nextNode;
	return 0;
}

static int freeNode(pfile *table)
{
	pfile cache = *table;
	while (cache != NULL)
	{
		pfile temp = cache;
		cache = cache->next;
		free(temp);
	}
	*table = NULL;
	return 0;
}

static int path_process(const char *file_name, const struct stat *sb, int flag)
{
	if ((flag == FTW_D || flag == FTW_DNR || flag == FTW_DP) && !KMP(file_name, search_pattern))
	{
		addNode(&file_list, file_name, 'D'); //Directory.
	}
	else if (flag == FTW_F && !KMP(file_name, search_pattern))
	{
		addNode(&file_list, file_name, 'F'); //Normal File.
	}
	else if ((flag == FTW_SL || flag == FTW_SLN) && !KMP(file_name, search_pattern))
	{
		addNode(&file_list, file_name, 'L'); //Symbolic Link.
	}
	else if (!KMP(file_name, search_pattern))
	{
		addNode(&file_list, file_name, 'U');  //Unknown.
	}
	return 0;
}

DLL_EXPORT pfile __stdcall find(char *workdir, char *pattern)
{
	freeNode(&file_list);
	memset(search_pattern, '\0', sizeof(search_pattern));
	strcpy(search_pattern, pattern);
	ftw(workdir, path_process, 1000);

	return file_list;
}
