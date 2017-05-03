def print_list(args):
    SCOPE_DICT = {"state": "stid", "county": "ctid", "metro": "mid"}
    from tabulate import tabulate  # Just for testing
    from collections import OrderedDict as OD

    def feed_dicts_to_table(l):
        return OD((k, [i[k] for i in l]) for k in l[0])

    if args.type == "states":
        print(tabulate(search.get_ids("", "stid").items(),
                       headers=["State", "ID"]))
    else:
        if not (args.id and args.scope):
            parser.error("must supply scope with -s/--scope and "
                         "scope id with --id")
        elif args.type == "feeds":
            path = "{}/{}".format(SCOPE_DICT[args.scope], args.id)
            print(path)
            print(tabulate(feed_dicts_to_table(search.get_feeds(path)),
                           headers="keys"))


def play_feed(args):
    raise NotImplementedError


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    actions = parser.add_subparsers(title="actions", dest="action")
    parser.set_defaults(func=None)

    parser_list = actions.add_parser("list", aliases=["l"],
                                     help="Lists entities")
    parser_list.add_argument("-s", "--scope", help="Specifies the scope for -l",
                             choices=["state", "county", "metro"],
                             metavar="S")
    parser_list.add_argument("--id", type=int,
                             help="Specifies stid, cid, or mid",
                             default=0, nargs="?")
    parser_list.add_argument("type", help="The type to be listed",
                             choices=["states", "counties", "metros", "feeds"])
    parser_list.set_defaults(func=print_list)

    parser_play = actions.add_parser("play", aliases=["p"], help="Play feed")
    parser_play.add_argument("feed_id", help="Specifies feed id", type=int)
    parser_play.set_defaults(func=play_feed)

    args = parser.parse_args()
    if args.func:
        import search
        args.func(args)
    else:
        parser.print_help()
