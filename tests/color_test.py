import time


YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print(f'{YELLOW}This is yellow!{NC}\nThis is not')
print('Next line')

for i in range(10):
    time.sleep(1)
    end = 'e' * (10-i)
    print(f'\033[AWriting line{end}: {YELLOW}{i + 1}{NC}\033[K')