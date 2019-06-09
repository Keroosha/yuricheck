#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <jerasure.h>
#include <jerasure/reed_sol.h>

#define talloc(type, num) (type *) malloc(sizeof(type)*(num))

static void usage(char *s)
{
  fprintf(stderr, "usage: reedsolo k m\n");
  fprintf(stderr, "encode k bytes into k + m bytes, where k + m <= 256\n");
  if (s != NULL) fprintf(stderr, "\nerror: %s\n", s);
  exit(1);
}

static ssize_t readall(int fd, void *buf, size_t count) {
  int n = 0;
  while (n < count) {
    ssize_t r;
    if ((r = read(fd, buf + n, count - n)) < 0) {
      return r;
    }
    n += r;
  }
  return n;
}

static ssize_t writeall(int fd, void *buf, size_t count) {
  int n = 0;
  while (n < count) {
    ssize_t r;
    if ((r = write(fd, buf + n, count - n)) < 0) {
      return r;
    }
    n += r;
  }
  return n;
}

int main(int argc, char **argv)
{
  int w = 8;

  int k, m;
  if (argc != 3) usage(NULL);
  if (sscanf(argv[1], "%d", &k) == 0 || k <= 0) usage("bad k");
  if (sscanf(argv[2], "%d", &m) == 0 || m <= 0) usage("bad m");
  if (k + m > (1 << w)) usage("k + m is too big");

  int *matrix = reed_sol_vandermonde_coding_matrix(k, m, w);

  char *raw_data = talloc(char, k + m);
  int r;
  if ((r = readall(STDIN_FILENO, raw_data, k)) < 0) {
    perror("while reading data");
    return r;
  }

  char **data = talloc(char *, k);
  for (int i = 0; i < k; i++) {
    data[i] = raw_data + i;
  }
  char **coding = talloc(char *, m);
  for (int i = 0; i < m; i++) {
    coding[i] = raw_data + k + i;
  }

  jerasure_matrix_encode(k, m, w, matrix, data, coding, sizeof(char));

  if ((r = writeall(STDOUT_FILENO, raw_data, k + m)) < 0) {
    perror("while writing data");
    return r;
  }

  return 0;
}
