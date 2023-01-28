#include <sys/stat.h>

typedef struct File_type
{
	struct File_type *next;
	time_t edit_time;
	off_t file_size;
	char file_name[261];
	char file_type;
}file, *pfile;

#ifndef __REFINDER_ENGINE_H__
#define __REFINDER_ENGINE_H__

#ifdef BUILD_DLL
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT __declspec(dllimport)
#endif

#ifdef __cplusplus
extern "C" {
#endif
    DLL_EXPORT pfile __stdcall find(char *workdir, char *pattern);
    DLL_EXPORT unsigned long long __stdcall return_files_count(void);
#ifdef __cplusplus
}
#endif

#endif
