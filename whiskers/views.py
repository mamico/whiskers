import json
import transaction
from pyramid.response import Response
from whiskers.models import DBSession
from whiskers.models import Buildout, Package, Version
from pyramid.renderers import get_renderer


def whiskers_view(request):
    main = get_renderer('whiskers:templates/master.pt').implementation()
    return {'project':'whiskers', 'main': main}


def add_buildout_view(request):
    try:
        data = json.loads(request.params['data'])
    except KeyError:
        return Response('No data. Nothing added.')

    session = DBSession()
    buildoutname = data['buildoutname']
    packages = data['packages']
    prepared_packages = prepare_packages(session,packages)
    buildout = session.query(Buildout).filter_by(name=buildoutname)

    if not buildout.count():
        buildout = Buildout(name=buildoutname, packages=prepared_packages)
    else:
        buildout = buildout[0]
        buildout.packages = prepared_packages
    session.merge(buildout)
    transaction.commit()
    return Response('OK')


def prepare_packages(session, packages):
    packages_list = list()
    for package in packages:
        existing_version = session.query(Version).filter_by(version=package['version'])
        existing_package = None
        if existing_version.count():
            version = existing_version.first()
            existing_package = session.query(Package).filter_by(name=package['name'],
                                                   version=version)
        else:
            version = Version(package['version'])

        if not existing_package:
            package_item = Package(package['name'], version)
        else:
            package_item = existing_package.first()
        packages_list.append(package_item)
    return packages_list

def buildouts_view(request):
    main = get_renderer('whiskers:templates/master.pt').implementation()
    session = DBSession()
    buildouts = session.query(Buildout).all()
    return {'buildouts': buildouts, 'project':'whiskers', 'main': main}

def buildout_view(request):
    main = get_renderer('whiskers:templates/master.pt').implementation()
    session = DBSession()
    buildout_id = request.matchdict['buildout_id']
    buildout = session.query(Buildout).filter_by(id=int(buildout_id)).one()
    return {'buildout': buildout, 'project':'whiskers', 'main': main}

def package_view(request):
    main = get_renderer('whiskers:templates/master.pt').implementation()
    session = DBSession()
    package_id = request.matchdict['package_id']
    package = session.query(Package).filter_by(id=int(package_id)).one()
    return {'package': package, 'project':'whiskers', 'main': main}

def packages_view(request):
    main = get_renderer('whiskers:templates/master.pt').implementation()
    session = DBSession()
    packages = session.query(Package).all()
    return {'packages': packages, 'project':'whiskers', 'main': main}
