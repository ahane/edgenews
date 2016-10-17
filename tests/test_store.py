import pytest

from edgenews import store

@pytest.fixture(scope='module')
def repo():
    return store.MemoryRepository('dummy')

@pytest.fixture
def one_record():
    return {'name': 'bert'}

@pytest.fixture
def another_record():
    return {'name': 'hans'}

def test_put_memory(repo, one_record, another_record):
    repo.save(one_record)
    repo.save(another_record)
    assert len(repo._records)

def test_get_memory(repo, one_record):
    retrieved = repo.first('name', 'hans')
    assert retrieved['name'] == 'hans'
