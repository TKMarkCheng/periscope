from setuptools import setup
from periscope_multi import __version__, _program

setup(
    name='periscope_multi',
    version=__version__,
    packages=['periscope'],
    scripts=['periscope/scripts/Snakefile',
             'periscope/scripts/search_for_sgRNA_ont.py',
             'periscope/scripts/search_for_sgRNA_illumina.py',
             'periscope/scripts/variant_expression.py',
             'periscope/scripts/create_multi_reference.py',
             'periscope/scripts/search_old.py'
             ],
    package_dir={'periscope_multi': 'periscope_multi'},
    package_data={'periscope_multi':['resources/*']},
    url='',
    license='',
    author='Thomas Baudeau,Matthew Parker',
    author_email='thomas.baudeau@univ-lille.fr',
    description='periscope_multi searches for and quanifies sgRNAs in SARS-CoV-2 from a fork of periscope',
    entry_points="""
    [console_scripts]
    {program} = periscope_multi.periscope_multi:main
    """.format(program=_program),
    include_package_data=True,
)

