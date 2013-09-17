import nazs

def common(request):
    """
    NAZS common context processor
    """
    return {
        'nazs': {
            'modules': nazs.modules(),
        },
    }
