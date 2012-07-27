import sys

if sys.version_info[0] < 2 and sys.version_info[1] < 6:
    print("Python version 2.6 or higher is required")
    exit(1)

try:
    import pyglet
    pyglet.sprite
except (ImportError, AttributeError):
    print("Pyglet 1.2alpha1 or greater is required")
    raise

import traceback
import tempfile
import infodump
import target

LOG_BOUNDARY = "\n%s\n\n" % ("=" * 72)

def main():
    target.Target().start()

if __name__ == '__main__':
    logfile = None
    try:
        main()
    except Exception as e:
        logfile = tempfile.NamedTemporaryFile(suffix='.log', prefix='crashdump-', dir='.', mode='w', delete=False)
        logfile.write("CLOSED WITH EXCEPTION\n\n")
        traceback.print_exc(file=logfile)
        logfile.write(LOG_BOUNDARY)
        print("Crashed, please see %s" % logfile.name)
    finally:
        try:
            infodump.init()
            if not logfile:
                logfile = open('infodump.log', 'w')
            logfile.write(infodump.pretty_results)
            logfile.close()
        except:
            print("Error creating infodump")
            raise
        
