
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_languages(cldf_dataset):
    # paper say 42 but 5 have no data:
    # - BackhouseWalker
    # - Fisher
    # - Lhotsky
    # - PeronBaudin
    # - SterlingNorman
    assert len(list(cldf_dataset["LanguageTable"])) == 42 - 5


def test_forms(cldf_dataset):
    assert len([
        f for f in cldf_dataset['FormTable'] if f['Form'] == 'win.co.parl.der.re'
    ]) == 1


def test_parameters(cldf_dataset):
    # we should have 644 parameters, but we lose some as they seem to be in language
    # "unknown15", which we can't identify
    assert len(list(cldf_dataset["ParameterTable"])) == 629


def test_sources(cldf_dataset):
    assert len(cldf_dataset.sources) == 1
