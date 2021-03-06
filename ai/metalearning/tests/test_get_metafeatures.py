import unittest
from unittest.mock import Mock, patch
from nose.tools import nottest, raises, assert_equals, assert_in, assert_not_in, assert_is_none
from parameterized import parameterized
import ai.metalearning.get_metafeatures as mf
import pandas as pd
from ai.metalearning.dataset_describe import Dataset
import os
import simplejson
import logging
import sys
import os
import io

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.environ["PROJECT_ROOT"] = "/appsrc"

package_directory = os.path.dirname(os.path.abspath(__file__))


@nottest
def main_args_good():
    return [
            (os.path.join(package_directory, 'iris.csv'),
            'Name',
            'filepath'),
            (os.path.join(package_directory, 'iris.csv'),
            'Name',
            None),
    ]

def main_args_bad():
    return [
            (os.path.join(package_directory, 'iris.csv'),
            'Namezzz',
            'filepath')
    ]


class Dataset_Describe(unittest.TestCase):

    def setUp(self):
        self.irisPath = os.path.join(package_directory, 'iris.csv')
        self.irisTarget = "Name"

        self.tipsPath = os.path.join(package_directory, 'tips.csv')

        #dataset that contains string values
        self.appendicitisStringPath = os.path.join(package_directory, 'appendicitis_cat_ord.csv')

        #row permutation of the iris dataset
        self.irisPermutePath = os.path.join(package_directory, 'iris_permute.csv')

        self.depColMetafeature = "_dependent_col"

        self.expectedMetafeatureKeys = [
            "_id",
            "_dependent_col",
            "_metafeature_version",
            "_categorical_cols",
            "_independent_cols",
            "_data_hash",
            "_prediction_type",
            "n_rows",
            "n_columns",
            "ratio_rowcol",
            "n_categorical",
            "n_numerical",
            "n_classes",
            "corr_with_dependent_abs_max",
            "corr_with_dependent_abs_min",
            "corr_with_dependent_abs_mean",
            "corr_with_dependent_abs_median",
            "corr_with_dependent_abs_std",
            "corr_with_dependent_abs_25p",
            "corr_with_dependent_abs_75p",
            "corr_with_dependent_abs_kurtosis",
            "corr_with_dependent_abs_skew",
            "class_prob_min",
            "class_prob_max",
            "class_prob_std",
            "class_prob_mean",
            "class_prob_median",
            "symbols_mean",
            "symbols_std",
            "symbols_min",
            "symbols_max",
            "symbols_sum",
            "symbols_skew",
            "symbols_kurtosis",
            "kurtosis_mean",
            "kurtosis_median",
            "kurtosis_min",
            "kurtosis_max",
            "kurtosis_std",
            "kurtosis_kurtosis",
            "kurtosis_skew",
            "skew_mean",
            "skew_median",
            "skew_min",
            "skew_max",
            "skew_std",
            "skew_kurtosis",
            "skew_skew",
            "pca_fraction_95",
            "entropy_dependent",
            "diversity_fraction",
        ]

    def test_generate_metafeatures(self):
        irisPd = pd.read_csv(self.irisPath, sep=None, engine='python')
        irisDs = Dataset(irisPd, dependent_col = self.irisTarget, prediction_type='classification')

        self.assertTrue(irisDs)

        result = mf.generate_metafeatures(irisDs)
        self.assertEquals(set(result.keys()), set(self.expectedMetafeatureKeys))
        self.assertEquals(result[self.depColMetafeature], self.irisTarget)


    def test_generate_metafeatures_from_filepath(self):
        result = mf.generate_metafeatures_from_filepath(self.irisPath, self.irisTarget)
        self.assertEquals(set(result.keys()), set(self.expectedMetafeatureKeys))
        self.assertEquals(result[self.depColMetafeature], self.irisTarget)
    @parameterized.expand(main_args_good)
    def test_validate_main_good(self, file_path, target, identifier_type):
        result = io.StringIO()
        testargs = ["program.py", file_path]

        if target: testargs.extend(['-target', target])
        if identifier_type: testargs.extend(['-identifier_type', identifier_type])

        logger.debug("testargs: " + str(testargs))

        with patch.object(sys, 'argv', testargs):
            sys.stdout = result
            mf.main()
            sys.stdout = sys.__stdout__

        logger.debug(f'result:\n=====\n{result.getvalue()}\n=====')

        self.assertTrue(result.getvalue())
        
        objResult = None
        try:
            objResult = simplejson.loads(result.getvalue())
        except simplejson.JSONDecodeError as e:
            self.assertIsNone(e)

        self.assertIsInstance(objResult, dict)
        self.assertNotIn("success", objResult.keys())
        self.assertIn("n_classes", objResult.keys())


    @parameterized.expand(main_args_bad)
    def test_validate_main_bad(self, file_path, target, identifier_type):
        result = io.StringIO()
        testargs = ["program.py", file_path]

        if target: testargs.extend(['-target', target])
        if identifier_type: testargs.extend(['-identifier_type', identifier_type])

        logger.debug("testargs: " + str(testargs))

        with patch.object(sys, 'argv', testargs):
            sys.stdout = result
            mf.main()
            sys.stdout = sys.__stdout__

        logger.debug(f'result:\n=====\n{result.getvalue()}\n=====')

        self.assertTrue(result.getvalue())
        
        objResult = None
        try:
            objResult = simplejson.loads(result.getvalue())
        except simplejson.JSONDecodeError as e:
            self.assertIsNone(e)

        self.assertIsInstance(objResult, dict)
        self.assertIn("success", objResult.keys())
        self.assertFalse(objResult['success'])