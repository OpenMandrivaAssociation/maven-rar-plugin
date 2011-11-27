Name:           maven-rar-plugin
Version:        2.2
Release:        6
Summary:        Plugin to create Resource Adapter Archive which can be deployed to a J2EE server

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-rar-plugin/
# svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-rar-plugin-2.2/
# tar jcf maven-rar-plugin-2.2.tar.bz2 maven-rar-plugin-2.2/
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: plexus-utils
BuildRequires: ant-nodeps
BuildRequires: maven2
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: jpackage-utils
Requires: ant-nodeps
Requires: maven2
Requires: jpackage-utils
Requires: java
Requires(post): jpackage-utils
Requires(postun): jpackage-utils 

Obsoletes: maven2-plugin-rar <= 0:2.0.8
Provides: maven2-plugin-rar = 1:%{version}-%{release}

%description
A resource adapter is a system-level software driver that 
a Java application to connect to an enterprise 
information system (EIS).The RAR plugin has the capability 
to store these resource adapters to an archive 
(Resource Adapter Archive or RAR) which can be deployed to
 a J2EE server.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires: jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q #You may need to update this according to your Source0

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository

#FIXME: mvn-jpp doesn't build jar "maven-rar-plugin-2.2/target/unit/basic-rar-test/target/test-rar.rar", why?
mvn-jpp \
        -e \
        -Dmaven.test.failure.ignore=true \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins %{name} %{version} JPP %{name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

