#!/usr/bin/env python3

import random as R
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import numpy as np

def linear_search( things, sought ):
    idx = 0
    for thing in things:
        if thing == sought:
            return idx
        idx += 1
    return None

def binary_search( things, sought ):
    low = 0
    high = len( things ) - 1
    while high >= low:
        mid = ( low + high ) // 2
        thing = things[ mid ]
        if thing < sought:
            high = mid - 1
        elif thing > sought:
            low = mid + 1
        else:
            return mid
    return None

def search_timing_test( f, small, large, grow, tests_per_size, density ):
    arr_size = small
    arr_sizes = []
    times = []
    while arr_size < large:
        num_range = arr_size * density
        nums = []
        for i in range( arr_size ):
            nums.append( R.randrange( num_range ) )
        nums.sort()

        start = timer()
        for i in range( tests_per_size ):
            test_num = R.randrange( num_range )
            idx_maybe = f( nums, test_num )
        end = timer()
        # diff is in units of seconds
        diff = end - start
        arr_sizes.append( arr_size )
        time_per_search = diff / tests_per_size
        times.append( time_per_search )
        # print( "'N'=%d time=%s" %( arr_size, diff ) )

        arr_size *= grow
    return ( arr_sizes, times )

def main():
    R.seed( 42 )
    ( xs1, ys1 ) = search_timing_test( linear_search,  10000, 1000000, 2,   10, 2 )
    ( xs2, ys2 ) = search_timing_test( binary_search, 100000, 20000000, 2, 100000, 2 )
    xs3 = np.array( range( 1000000 ) )
    ys3 = xs3
    ys4 = np.log2( xs3 )
    plt.plot( xs1, ys1, label='linear' )
    plt.plot( xs2, ys2, label='binary' )
    plt.plot( xs3, ys3, label='O(n)' )
    plt.plot( xs3, ys4, label='O(n log( n ) )' )
    plt.xlim( 0, 1000 )
    plt.ylim( 0, 1000 )
    plt.xlabel('Array Sizes')
    plt.ylabel( 'Run Times' )
    plt.legend()
    plt.show()

main()
