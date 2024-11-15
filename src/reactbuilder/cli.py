import argparse, os
from reactbuilder import put_in_tempdir, build_site, collect_artifacts

def main(argv=None):
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'react_dir',
		type=str,
		help='Directory containing package.json'
	)
	parser.add_argument(
		'--skip_install',
		action='store_true',
		help='Skip the npm install step for speed.'
	)
	parser.add_argument(
		'--temp_dir', type=str, default=None,
		required=False,
	)
	parser.add_argument(
		'--build_parent',
		type=str, required=False,
		default=None,
		help='Destination for build artifacts. Will default to react_dir.',
	)
	parser.add_argument(
		'--delete_existing',
		action='store_true',
		help='Whether we should delete existing package-lock.json and node_modules under the temp dir.',
	)

	if argv is not None:
		args = parser.parse_args(argv)
	else:
		args = parser.parse_args()
		
	if args.build_parent is None:
		args.build_parent = args.react_dir

	prev_tempdir = None
	if args.temp_dir is not None and os.path.exists(args.temp_dir):
		prev_tempdir = args.temp_dir

	args.temp_dir = put_in_tempdir(
		args.react_dir,
		prev_tempdir=prev_tempdir,
		delete_existing=args.delete_existing,
	)
	print(f"temp_dir: {args.temp_dir}")

	build_result = build_site(args.temp_dir, do_install=not args.skip_install)
	print(f"build_result: {build_result}")

	collected_dest = collect_artifacts(args.temp_dir, args.build_parent)
	print(f"collected_dest: {collected_dest}")

if __name__ == "__main__":
	main()