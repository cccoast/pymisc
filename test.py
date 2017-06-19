from multiprocessing import Pool
import time

if __name__ == '__main__':
    
    def sleep_and_print(seconds):
        time.sleep(seconds)
        print seconds
        
    p = Pool(5)
    print(p.map(sleep_and_print, [1, 2, 3, 4, 5]))
               
    print 'all done!'