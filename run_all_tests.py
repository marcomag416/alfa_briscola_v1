import os
import subprocess

def run_all_tests():
    test_dir = './tests'
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith('.py'):
                print(f'Running test {file}')
                file_path = os.path.join(root, file)
                subprocess.run(['python', file_path])

if __name__ == '__main__':
    run_all_tests()