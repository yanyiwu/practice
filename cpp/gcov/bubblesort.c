#include <stdio.h>

void bubbleSort( int list[], int size )
{
    int i, j, temp, swap = 1;

    while (swap) {

        swap = 0;

        for ( i = (size-1) ; i >= 0 ; i--) {

            for ( j = 1 ; j <= i ; j++ ) {

                if ( list[j-1] > list[j] ) {

                    temp = list[j-1];
                    list[j-1] = list[j];
                    list[j] = temp;
                    swap = 1;

                }

            }

        }

    }

}

void func2() {
    printf("\n");
}

int main()
{
    int theList[10]={10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
    int i;

    /* Invoke the bubble sort algorithm */
    bubbleSort( theList, 10 );

    /* Print out the final list */
    for (i = 0 ; i < 10 ; i++) { 
        printf("%d\n", theList[i]);
    }

}
