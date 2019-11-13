def fpatterns(tt):
    patterns = ['txt', 'csv', 'pdf']
    import os
    for f in os.listdir(tt):
        if any(pattern in f for pattern in patterns):
            print(f)
            try:
                os.remove(os.path.join(tt, f))
            except OSError:
                print("there's no such a file")