#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests (missing in sdist)

Summary:	Useful decorators and context managers
Name:		python3-jaraco.context
Version:	6.0.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco.context/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco.context/jaraco_context-%{version}.tar.gz
# Source0-md5:	bb22ef027077b1fa8528ef1d9840b838
URL:		https://pypi.org/project/jaraco.context/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:56
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-pytest >= 6
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 9
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3 >= 3.5
#BuildRequires:	sphinx-lint
%endif
Requires:	python3-jaraco
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Useful decorators and context managers.

%package apidocs
Summary:	API documentation for Python jaraco.context module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jaraco.context
Group:		Documentation

%description apidocs
API documentation for Python jaraco.context module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jaraco.context.

%prep
%setup -q -n jaraco_context-%{version}

# stub for setuptools
cat >setup.py <<EOF
from setuptools import setup
setup()
EOF

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=... \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst NEWS.rst
%{py3_sitescriptdir}/jaraco/context
%{py3_sitescriptdir}/jaraco.context-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
