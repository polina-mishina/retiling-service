def get_url(provider_name, level, resolution, z, x, y):
    url = '/retile/{provider_name}/{level}/{resolution}/{z}/{x}/{y}.png'.format(
        provider_name=provider_name,
        level=level,
        resolution=resolution,
        z=z,
        x=x,
        y=y,
    )
    return url


def test_zoom_in(client):
    url = get_url(provider_name='google', level=2, resolution=512, z=5, x=28, y=12)
    res = client.get(url)
    file_name = 'tile_{level}_{resolution}_{z}_{x}_{y}.png'.format(
        level=2,
        resolution=512,
        z=5,
        x=28,
        y=12
    )
    save_file = open(file_name, "wb")
    save_file.write(res.data)
    save_file.close()
    assert res.status_code == 200

    url = get_url(provider_name='google', level=20, resolution=512, z=5, x=28, y=12)
    res = client.get(url)
    assert res.status_code == 500


def test_zoom_out(client):
    url = get_url(provider_name='google', level=-2, resolution=512, z=5, x=28, y=12)
    res = client.get(url)
    file_name = 'tile_{level}_{resolution}_{z}_{x}_{y}.png'.format(
        level=-2,
        resolution=512,
        z=5,
        x=28,
        y=12
    )
    save_file = open(file_name, "wb")
    save_file.write(res.data)
    save_file.close()
    assert res.status_code == 200

    url = get_url(provider_name='google', level=-10, resolution=512, z=14, x=10245, y=5263)
    res = client.get(url)
    assert res.status_code == 500

    url = get_url(provider_name='google', level=-10, resolution=512, z=5, x=28, y=12)
    res = client.get(url)
    assert res.status_code == 500


def test_zoom_not_change(client):
    url = get_url(provider_name='google', level=0, resolution=512, z=5, x=28, y=12)
    res = client.get(url)
    file_name = 'tile_{level}_{resolution}_{z}_{x}_{y}.png'.format(
        level=0,
        resolution=512,
        z=5,
        x=28,
        y=12
    )
    save_file = open(file_name, "wb")
    save_file.write(res.data)
    save_file.close()
    assert res.status_code == 200


def test_input_param(client):
    url = get_url(provider_name='openstreetmap', level=2, resolution=512, z=5, x=28, y=12)
    res = client.get(url)
    assert res.status_code == 422

    url = get_url(provider_name='google', level=2, resolution=0, z=5, x=28, y=12)
    res = client.get(url)
    assert res.status_code == 422

    url = get_url(provider_name='google', level=2, resolution=-125, z=5, x=28, y=12)
    res = client.get(url)
    assert res.status_code == 422

    url = get_url(provider_name='google', level=2, resolution=512, z=-1, x=28, y=12)
    res = client.get(url)
    assert res.status_code == 422

    url = get_url(provider_name='google', level=0, resolution=512, z=23, x=28, y=12)
    res = client.get(url)
    assert res.status_code == 422

    url = get_url(provider_name='google', level=2, resolution=512, z=5, x=-28, y=12)
    res = client.get(url)
    assert res.status_code == 422

    url = get_url(provider_name='google', level=2, resolution=512, z=5, x=28, y=-12)
    res = client.get(url)
    assert res.status_code == 422
