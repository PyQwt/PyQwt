#include <stdio.h>
#include <qwt_global.h>

int main(int, char **)
{
    FILE *file;

    if (!(file = fopen("qwt_version_info.py", "w"))) {
	fprintf(stderr, "Failed to create qwt_version_info.py\n");
	return 1;
    }
	
    fprintf(file, "QWT_VERSION = %#08x\n", QWT_VERSION);
    fprintf(file, "QWT_VERSION_STR = '%s'\n", QWT_VERSION_STR);

    fclose(file);

    return 0;
}

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
