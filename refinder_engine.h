typedef struct File_type
{
	struct File_type *next;
	char file_type;
	char file_name[261];
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
#ifdef __cplusplus
}
#endif

#endif
