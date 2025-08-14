#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LINE 200
#define TEMPLATE_FILE "template.docx"
#define OUTPUT_DIR "./output/" // make sure this directory exists

void trim_newline(char* str) {
    size_t len = strlen(str);
    if (len && (str[len - 1] == '\n' || str[len - 1] == '\r'))
        str[len - 1] = '\0';
}

// Replace spaces with underscores, but keep UTF-8 characters intact
void sanitize_filename(char* str) {
    unsigned char* p = (unsigned char*)str;

    while (*p) {
        if (*p == ' ') {
            *p = '_';
        }
        // Otherwise, leave character as-is, including UTF-8 multibyte
        p++;
    }
}

void copy_file(const char* src, const char* dest) {
    FILE *in = fopen(src, "rb");
    FILE *out = fopen(dest, "wb");

    if (!in || !out) {
        fprintf(stderr, "Error opening files: %s -> %s\n", src, dest);
        exit(1);
    }

    char buffer[4096];
    size_t bytes;
    while ((bytes = fread(buffer, 1, sizeof(buffer), in)) > 0) {
        fwrite(buffer, 1, bytes, out);
    }

    fclose(in);
    fclose(out);
}

int main() {
    FILE* name_file = fopen("names.txt", "r");
    if (!name_file) {
        perror("Could not open names.txt");
        return 1;
    }

    char line[MAX_LINE];
    while (fgets(line, sizeof(line), name_file)) {
        trim_newline(line);

        if (strlen(line) == 0) continue;  // skip empty lines

        // Create a sanitized filename
        char safe_name[MAX_LINE];
        strncpy(safe_name, line, MAX_LINE);
        sanitize_filename(safe_name);  // e.g. "Alice Smith" -> "Alice_Smith"

        char filename[MAX_LINE + 100];
        snprintf(filename, sizeof(filename), OUTPUT_DIR"%s.docx", safe_name);

        copy_file(TEMPLATE_FILE, filename);
        printf("Created: %s\n", filename);
    }

    fclose(name_file);
    return 0;
}
