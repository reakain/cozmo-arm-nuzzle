import pycozmo

def main():
    with pycozmo.connect() as cli:
        cli.drive_wheels(100,-100, lwheel_acc=999, rwheel_acc=999, duration = 0.3)

if __name__ == "__main__":
    main()