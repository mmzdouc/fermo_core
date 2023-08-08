"""Direct the creation of a dict of generalized features


TODO(MMZ): Improve description of class


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

from typing import Dict
from fermo_core.input_output.dataclass_params_handler import ParamsHandler


class GeneralFeatureDirector:
    """Builds the general feature instances"""

    @staticmethod
    def construct(params: ParamsHandler) -> Dict:
        """Constructs the products and returns them in a dict.

        Args:
            params: an instance of the ParamsHandler class, holding user input

        Returns:
            A dict containing instances of the GeneralFeature class.
        """
        # load the peaktable
        # loop over the peaktable and extract the entries to create the instance
        # collect in dict
        # return dict

        feature_dict = dict()

        # pro forma test if it works
        # feature_dict[1] = FeatureBuilder()\
        #     .set_f_id(1)\
        #     .set_mz(101.1)\
        #     .get_result()

        return feature_dict
