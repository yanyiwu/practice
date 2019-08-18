from util import load_images_data_batch

def main():
    for d in load_images_data_batch():
        print d
        print d.shape

if __name__ == '__main__':
    main()
