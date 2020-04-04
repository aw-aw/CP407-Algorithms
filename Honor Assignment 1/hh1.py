import random as R
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import numpy as np

R.seed( 1 )

def insertionSort( unsorted ):
    for i in range( len( unsorted ) ):
        curr_pos = i
        for j in reversed( range( 0, i ) ):
            if unsorted[ curr_pos ] < unsorted[ j ]:
                temp = unsorted[ curr_pos ]
                unsorted[ curr_pos ] = unsorted[ j ]
                unsorted[ j ] = temp
                curr_pos -= 1
            else:
                break
    return unsorted

def mergeSortHelper( list1, list2 ):
    sorted = []
    while len( list1 ) > 0 and len( list2 ) > 0:
        if list1[ 0 ] > list2[ 0 ]:
            sorted.append( list2[ 0 ] )
            del list2[ 0 ]
        else:
            sorted.append( list1[ 0 ] )
            del list1[ 0 ]
    if len( list1 ) > 0:
        for element in list1:
            sorted.append( element )
    else:
        for element in list2:
            sorted.append( element )
    return sorted

def mergeSort( unsorted ):
    if len( unsorted ) == 1:
        return unsorted
    else:
        left_list = unsorted[ : len( unsorted ) // 2 ]
        right_list = unsorted[ len( unsorted ) // 2 : ]
        return mergeSortHelper( mergeSort( left_list ), mergeSort( right_list ) )

def timsort( unsorted, threshold ):
    if len( unsorted ) <= threshold:
        return insertionSort( unsorted )
    else:
        left_list = unsorted[ : len( unsorted ) // 2 ]
        right_list = unsorted[ len( unsorted ) // 2 : ]
        return mergeSortHelper( timsort( left_list, threshold ), timsort( right_list, threshold ) )

def createReverseSortedData( n ):
    out_list = []
    for i in reversed( range( n ) ):
        out_list.append( i )
    return out_list

def createSortedData( n ):
    out_list = []
    for i in range( n ):
        out_list.append( i )
    return out_list

def createRandomData( min, max, n ):
    out_list = R.sample( range( min, max ), n )
    return out_list

def timeSortHelperTim( f, threshold, small, large, grow, tests_per_size, density ):
    arr_size = small
    arr_sizes = []
    times = []
    while arr_size < large:
        input = createRandomData( 0, arr_size, arr_size )

        start = timer()

        for i in range( tests_per_size ):
            sorted = f( input, threshold )

        end = timer()
        diff = end - start
        arr_sizes.append( arr_size )
        times.append( diff / tests_per_size )

        print( "'N'=%d time=%s" %( arr_size, diff / tests_per_size ) )
        arr_size *= grow
    return ( arr_sizes, times )

def timeSortHelper( f, data_type, small, large, grow, tests_per_size, density ):
    arr_size = small
    arr_sizes = []
    times = []
    while arr_size < large:
        input = []
        if data_type == 0:
            input = createSortedData( arr_size )
        elif data_type == 1:
            input = createReverseSortedData( arr_size )
        else:
            input = createRandomData( 0, arr_size, arr_size )

        start = timer()

        for i in range( tests_per_size ):
            sorted = f( input )

        end = timer()
        diff = end - start
        arr_sizes.append( arr_size )
        times.append( diff / tests_per_size )

        print( "'N'=%d time=%s" %( arr_size, diff / tests_per_size ) )

        arr_size *= grow
    return ( arr_sizes, times )


def timeSort( f, small, large, grow, tests_per_size, density ):
    if f != timsort:
        print( "Sorting sorted input" )
        sorted_x, sorted_y = timeSortHelper( f, 0, small, large, grow, tests_per_size, density )
        print( "Sorting reversed input" )
        reversed_x, reversed_y = timeSortHelper( f, 1, small, large, grow, tests_per_size, density )
        print( "Sorting random input" )
        random_x, random_y = timeSortHelper( f, 2, small, large, grow, tests_per_size, density )

        plt.plot( sorted_x, sorted_y, label = "Sorted Inputs", linestyle = '-' )
        plt.plot( reversed_x, reversed_y, label = "Reversed Sorted Inputs", linestyle = '--' )
        plt.plot( random_x, random_y, label = "Random Inputs", linestyle = "-." )

        x = np.arange( 0, 10000 )
        y = x * np.log2( x )

        plt.plot( x, y, label = "O( n log( n ) )", linestyle = ":" )
        plt.xlim( 10000, 1000000 )
        plt.xlabel( "Input Sizes" )
        plt.ylabel( "Run Times" )
        plt.legend()
        plt.show()

timeSort( mergeSort, 10000, 1000000, 2, 10, 2 )


































#
