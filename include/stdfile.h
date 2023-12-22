#include <stdio.h>
#include <stdlib.h>

char *file_read(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file %s for reading.\n", filename);
        exit(EXIT_FAILURE);
    }

    // Determine the size of the file
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    // Allocate memory for the file content
    char *content = (char *)malloc(file_size + 1);

    if (content == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        exit(EXIT_FAILURE);
    }

    // Read the file content into the allocated memory
    fread(content, 1, file_size, file);

    // Null-terminate the string
    content[file_size] = '\0';

    // Close the file
    fclose(file);

    return content;
}

void file_write(const char *filename, const char *content) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        fprintf(stderr, "Error opening file %s for writing.\n", filename);
        return;
    }

    // Write the content to the file
    fprintf(file, "%s", content);

    // Close the file
    fclose(file);
}