import random as R
from timeit import default_timer as timer
import matplotlib.pyplot as plt

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

        print(f'N={arr_size} samples, time={diff / tests_per_size:.2f} seconds')
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

        print(f'N={arr_size} samples, time={diff / tests_per_size:.2f} seconds')
        # print( "'N'=%d time=%s" %( arr_size, diff / tests_per_size ) )

        arr_size *= grow
    return ( arr_sizes, times )

def timeSort( func_name, small, large, grow, tests_per_size, density ):
    sorts_dict = { "TimSort" : timsort, "Insertion Sort" : insertionSort, "Merge Sort" : mergeSort }
    xs = []
    ys = []
    labels = []
    linestyles = []
    if func_name != "TimSort":
        print( "Sorting sorted input" )
        sorted_x, sorted_y = timeSortHelper( sorts_dict.get( func_name, mergeSort ), 0, small, large, grow, tests_per_size, density )
        xs.append( sorted_x )
        ys.append( sorted_y )
        labels.append( func_name + " - Sorted" )
        linestyles.append( '-' )
        print( "Sorting reversed input" )
        reversed_x, reversed_y = timeSortHelper( sorts_dict.get( func_name, mergeSort ), 1, small, large, grow, tests_per_size, density )
        xs.append( reversed_x )
        ys.append( reversed_y )
        labels.append( func_name + " - Reversed" )
        linestyles.append( '--' )
        print( "Sorting random input" )
        random_x, random_y = timeSortHelper( sorts_dict.get( func_name, mergeSort ), 2, small, large, grow, tests_per_size, density )
        xs.append( random_x )
        ys.append( random_y )
        labels.append( func_name + " - Random" )
        linestyles.append( '-.' )

    else:
        thresholds = [ 1, 10, 100, 1000, 10000, 100000 ]
        lstyles = ['-', '--', '-.' ]
        for i in range( len( thresholds ) ):
            print( f"Sorting with threshold { thresholds[ i ] }" )
            random_x, random_y = timeSortHelperTim( sorts_dict.get( func_name, timsort ), thresholds[ i ], small, large, grow, tests_per_size, density )
            xs.append( random_x )
            ys.append( random_y )
            labels.append( func_name + " - TH" + str( thresholds[ i ] ) )
            linestyles.append( lstyles[ i % 3 ] )
    return xs, ys, labels, linestyles

def plotData( x_list, y_list, label_list, style_list, min, max ):
    for i in range( len( x_list ) ):
        plt.plot( x_list[ i ], y_list[ i ], label = label_list[ i ], linestyle = style_list[ i ] )
    plt.xlim( min, max )
    plt.xlabel( "Array Sizes" )
    plt.ylabel( "Run Times (s)" )
    plt.legend()
    plt.show()

xs = []
ys = []
labels = []
styles = []
small = 1
large = 10000

insert_xs, insert_ys, insert_labels, insert_ls = timeSort( "Insertion Sort", small, large, 2, 1, 2 )
merge_xs, merge_ys, merge_labels, merge_ls = timeSort( "Merge Sort", small, large, 2, 1, 2 )
tim_xs, tim_ys, tim_labels, tim_ls = timeSort( "TimSort", small, large, 2, 1, 2 )

for i in range( len( insert_xs ) ):
    xs.append( insert_xs[ i ] )
    ys.append( insert_ys[ i ] )
    labels.append( insert_labels[ i ] )
    styles.append( insert_ls[ i ] )

for i in range( len( merge_xs ) ):
    xs.append( merge_xs[ i ] )
    ys.append( merge_ys[ i ] )
    labels.append( merge_labels[ i ] )
    styles.append( merge_ls[ i ] )

for i in range( len( tim_xs ) ):
    xs.append( tim_xs[ i ] )
    ys.append( tim_ys[ i ] )
    labels.append( tim_labels[ i ] )
    styles.append( tim_ls[ i ] )

plotData( xs, ys, labels, styles, small, large )































#
