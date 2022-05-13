"""

    copy to Collab/JupyterNB as last cell and run all

"""

import signal

def signal_handler(signum, frame):
    raise Exception("timeout")

timeout = 5
signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(timeout)

passed, failed = 0, 0
optimal_rewards = {}         

algorithm_names = ["BFS", "DFS", "ID-DFS", "W-A*"]
algorithm_func  = [bfs, dfs, id_dfs, weighted_a_star]
algorithm_args  = [[], [], [0], [0.5, chosen_h]]

def algo_wrapper(func, args: list) -> tuple:
    return func(*args)

print("*** START TESTS WITH TIMEOUT={}sec ***".format(timeout))

for algo in range(4):
    print("START {} TESTS:".format(algorithm_names[algo]))
    fail_flag = False
    for state in range(500):
        signal.alarm(timeout)
        try:
            env.unwrapped.s = state
            frames, reward = algo_wrapper(algorithm_func[algo], [state] + algorithm_args[algo])
            if frames == []:
                failed += 1
                fail_flag = True
                print("   {} TEST #{}: FAILED (empty list)".format(algorithm_names[algo], state))
            else:
                if algo == 0:
                    optimal_rewards[state] = reward
                    passed += 1
                elif (algo == 2 or algo == 3) and optimal_rewards[state] != reward:
                    failed += 1
                    fail_flag = True
                    print("   {} TEST #{}: FAILED (not optimal)".format(algorithm_names[algo], state))
                else:
                    passed += 1
        except Exception as e:
            failed += 1
            fail_flag = True
            print("   {} TEST #{}: FAILED ({})".format(algorithm_names[algo], state, e))
    if not fail_flag:
        print("   all {} - PASSED".format(algorithm_names[algo]))

print("PASS: {}, FAIL: {}".format(passed , failed))