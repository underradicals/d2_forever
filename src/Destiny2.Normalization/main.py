from os import makedirs
import csv
from collections import deque
from pathlib import Path
from time import perf_counter
from typing import Mapping
from typing import Any
from os.path import join

from ijson import kvitems
from orjson import dumps
from loguru import logger

ROOT = 'G:\\Assets'
DATA = join(ROOT, 'Data')
FLATTENED = join(DATA, 'Flattened')
SEMI_FLATTENED = join(DATA, 'SemiFlattened')
PARQUET = join(DATA, 'Parquet')
RAW = join(DATA, 'Raw')
CSV = join(DATA, 'Csv')


def __flatten(data: Mapping[str, Any]) -> dict[str, Any]:
	result: dict[str, Any] = {}

	stack = deque([("", data)])

	while stack:
		path, value = stack.popleft()

		if isinstance(value, Mapping):
			for key, child in value.items():
				child_path = key if not path else f"{path}.{key}"
				stack.append((child_path, child))

		elif isinstance(value, list):
			for i, child in enumerate(value):
				child_path = f"{path}[{i}]"
				stack.append((child_path, child))

		else:
			result[path] = value

	return result


def flatten_dict(filepath: str | Path, output_path: str | Path) -> None:
	all_times = []
	result: dict[str, Any] = {}
	with open(filepath, 'rb') as f, open(output_path, 'wb') as o:
		for k, v in kvitems(f, ''):
			start_flattening = perf_counter()
			result.update(__flatten(v))
			end_flattening = perf_counter()
			all_times.append(end_flattening - start_flattening)
		logger.info("Flattened Dict at {} {:.2f}s", filepath, sum(all_times))
		o.write(dumps(result))


def get_keys():
	names = []
	with open(join(ROOT, "table_names.csv"), "r", encoding='UTF-8') as f:
		csv_reader = csv.reader(f, delimiter=',')
		for item in csv_reader:
			if item[0] == 'id':
				continue
			names.append(item[1])
	return names


def create_directories():
	makedirs(FLATTENED, exist_ok=True)
	makedirs(SEMI_FLATTENED, exist_ok=True)
	makedirs(PARQUET, exist_ok=True)
	makedirs(RAW, exist_ok=True)
	makedirs(CSV, exist_ok=True)


def main():
	create_directories()

if __name__ == "__main__":
	pass
