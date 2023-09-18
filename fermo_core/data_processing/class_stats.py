"""Storage and handling of general stats of analysis run.

***

Copyright (c) 2022-2023 Mitja Maximilian Zdouc, PhD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging

import pandas as pd
from typing import Self, Tuple, Optional, Set, Dict, List


class Stats:
    """Extract analysis run stats and organize them.

    Ad method nomenclature: each type of supported peaktable should have a separate
    parser method attributed to it that has the name of the peaktable in it.
    All methods addressing a peaktable format should mention it in method name.

    Attributes:
        rt_min: overall lowest retention time start across all samples, in minutes
        rt_max: overall highest retention time stop across all samples, in minutes
        rt_range: range in minutes between min and max rt.
        samples: all sample ids in analysis run
        features: all feature ids in analysis run in a tuple
        groups: a dict of lists containing sample ID strings to indicate membership in
            groups (if no explicit information, all samples in group "DEFAULT")
        cliques: all similarity cliques in analysis run
        phenotypes: all phenotype classifications in analysis run
        blank: all blank-associated features in analysis run
        int_removed: all features that were removed due to intensity range
        annot_removed: all features that were removed due to annotation range
        ms2_removed: feature IDs of which MS2 was removed
    """

    def __init__(self: Self):
        self.rt_min: Optional[float] = None
        self.rt_max: Optional[float] = None
        self.rt_range: Optional[float] = None
        self.samples: Optional[Tuple] = None
        self.features: Optional[Tuple] = None
        self.groups: Optional[Dict[str, Set[str | int]]] = {"DEFAULT": set()}
        self.cliques: Optional[Tuple] = None
        self.phenotypes: Optional[Tuple] = None
        self.blank: Optional[Tuple] = None
        self.int_removed: Optional[Tuple] = None
        self.annot_removed: Optional[Tuple] = None
        self.ms2_removed: Optional[List] = None

    def _get_features_in_range_mzmine3(
        self: Self, df: pd.DataFrame, r: Tuple[float, float]
    ) -> Tuple[Tuple, Tuple]:
        """Separate features into two sets based on their relative intensity.

        Filter features based on their relative intensity compared against the feature
        with the highest intensity in the sample. For a range between 0-1,
        for each feature, test if feature lies inside the given range in at least one
        sample. Only exclude features that are below the relative intensity in all
        samples in which they are detected.

        Args:
            df: pandas DataFrame resulting from mzmine3 style peaktable
            r: user-provided range

        Returns:
            Two tuples: one "included" (features inside of range), one "excluded" (
            features outside of range)
        """
        incl = set()
        excl = set()

        # Extract overall most intense feature per sample as ref for relative intensity
        sample_max_int = dict()
        for s in self.samples:
            sample_max_int[s] = df.loc[:, f"datafile:{s}:intensity_range:max"].max()

        for _, row in df.iterrows():
            # Get feature intensity per sample, prepare for comparison
            sample_values = row.dropna().filter(regex=":intensity_range:max")
            feature_int = dict()
            for index, value in sample_values.items():
                sample = index.split(":")[1]
                feature_int[sample] = value

            # Retain features that are inside rel int range for at least one sample
            if any(
                (sample_max_int[s] * r[0])
                <= feature_int[s]
                <= (sample_max_int[s] * r[1])
                for s in feature_int
            ):
                incl.add(row["id"])
            else:
                excl.add(row["id"])
                logging.info(
                    f"Molecular feature with feature ID '{row['id']}' was filtered "
                    f"from dataset due to range settings."
                )

        return tuple(incl), tuple(excl)

    @staticmethod
    def _extract_sample_names_mzmine3(df: pd.DataFrame) -> Tuple[str, ...]:
        """Extract sample names from mzmine3-style peaktable.

        Args:
            df: dataframe of mzmine3 style peaktable

        Returns:
            Tuple containing sample name strings.
        """
        samples = set()
        for s in df.filter(regex=":feature_state").columns:
            samples.add(s.split(":")[1])
        return tuple(samples)

    def parse_mzmine3(
        self,
        peaktable_path: str,
        rel_int_range: Tuple[float, float],
        ms2query_range: Tuple[float, float],
    ):
        """Parse a mzmine3 peaktable for general stats on analysis run.

        Args:
            peaktable_path: path to peaktable file
            rel_int_range: indicates range 0.0-1.0 to retain features in
            ms2query_range: indicates range 0.0-1.0 to retain features for ms2query ann

        Notes:
            All samples are grouped in group "DEFAULT".
        """
        df = pd.read_csv(peaktable_path)
        self.rt_min = df.loc[:, "rt_range:min"].min()
        self.rt_max = df.loc[:, "rt_range:max"].max()
        self.rt_range = self.rt_max - self.rt_min
        self.samples = self._extract_sample_names_mzmine3(df)
        self.groups["DEFAULT"] = set(self.samples)
        self.features, self.int_removed = self._get_features_in_range_mzmine3(
            df, rel_int_range
        )
        _, self.annot_removed = self._get_features_in_range_mzmine3(df, ms2query_range)
