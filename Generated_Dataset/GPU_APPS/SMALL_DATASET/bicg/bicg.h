/**
 * bicg.h: This file is part of the PolyBench/GPU 1.0 test suite.
 *
 *
 * Contact: Scott Grauer-Gray <sgrauerg@gmail.com>
 * Will Killian <killian@udel.edu>
 * Louis-Noel Pouchet <pouchet@cse.ohio-state.edu>
 * Web address: http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 */

#ifndef BICG_H
# define BICG_H

/* Default to STANDARD_DATASET. */
# if !defined(MINI_DATASET) && !defined(SMALL_DATASET) && !defined(LARGE_DATASET) && !defined(EXTRALARGE_DATASET)&& !defined(MINI_VVSMALL) && !defined(MINI_VSMALL) && !defined(MINI_SMALL)
#  define STANDARD_DATASET
# endif

/* Do not define anything if the user manually defines the size. */
# if !defined(NX) && !defined(NY)
/* Define the possible dataset sizes. */
#  ifdef MINI_VVSMALL
#define NX 128
#define NY 128
#  endif

#  ifdef MINI_VSMALL
#define NX 256
#define NY 256
#  endif

#  ifdef MINI_SMALL
#define NX 512
#define NY 512
#  endif


#  ifdef MINI_DATASET
#define NX 1024
#define NY 1024
#  endif

#  ifdef SMALL_DATASET
#define NX 2048
#define NY 2048
#  endif

#  ifdef STANDARD_DATASET /* Default if unspecified. */
#define NX 4096
#define NY 4096
#  endif

#  ifdef LARGE_DATASET
#define NX 8192
#define NY 8192
#  endif

#  ifdef EXTRALARGE_DATASET
#define NX 16384
#define NY 16384
#  endif
# endif /* !N */

# define _PB_NX POLYBENCH_LOOP_BOUND(NX,nx)
# define _PB_NY POLYBENCH_LOOP_BOUND(NY,ny)

# ifndef DATA_TYPE
#  define DATA_TYPE float
#  define DATA_PRINTF_MODIFIER "%0.2lf "
# endif

/* Thread block dimensions */
#define DIM_LOCAL_WORK_GROUP_X 256
#define DIM_LOCAL_WORK_GROUP_Y 1


#endif /* !BICG*/