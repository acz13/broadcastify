import argparse
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-s", "--scope", help="Specifies the scope for -l",
                    choices=["us", "state", "county", "metro"],
                    default="us", nargs="?", metavar="S")

parser.add_argument("id", type=int, help="Specifies stid, cid, mid or feed id",
                    default=0, nargs="?")

actions = parser.add_argument_group(title="actions")
actions.add_argument("-l", "--list", metavar="T",
                    help="Lists type T within scope",
                    choices=["states", "counties", "metros", "feeds"],
                    action="append", dest="actions")
actions.add_argument("-p", "--play", const="play",
                     help="Plays feed", action="append_const", dest="actions")

args = parser.parse_args()
if not args.actions:
    parser.error("one of the actions -l/--list -p/--play must be performed")
elif len(args.actions) > 1:
    parser.error("only one action may be performed")
action = args.actions[0]

if action == "play":
    raise NotImplementedError
else:
    raise NotImplementedError
