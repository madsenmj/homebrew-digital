int main(int num) {
    int t1 = 0;
    int t2 = 1;
    int nextterm = t1 + t2;
    int i = 0;
    while (i<num){
        t1 = t2;
        t2 = nextterm;
        nextterm = t1 + t2;
        i++;
    }
    return nextterm;
}