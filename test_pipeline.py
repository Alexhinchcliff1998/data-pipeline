from pipeline import normalize,run

def test_normalization():
    records=[{'id':1,'title':' Box ','category':' SHIPPING ','price':'12.123'},{'id':2,'title':'Bad','category':'x','price':'nan'},{'id':True,'title':'Invalid','category':'x','price':1}]
    assert normalize(records)==([(1,'Box','shipping',12.12)],2)

def test_repeatable_upsert(tmp_path):
    db=tmp_path/'test.db'
    assert run(database=db)==(2,1,2)
    assert run(database=db)==(2,1,2)
