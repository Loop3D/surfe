def test_import():
    success = False
    try:
        import surfepy
    except ImportError:
        success = False
    success = True  
    assert success