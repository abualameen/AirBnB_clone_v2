# puppet/manifests/init.pp

# Install Nginx
class { 'nginx':
  ensure => 'installed',
}

# Create necessary folders
file { ['/data/web_static/releases/test/', '/data/web_static/shared/']:
  ensure => 'directory',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>',
  require => File['/data/web_static/releases/test/'],
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
}

# Give ownership of the /data/ folder to the ubuntu user and group recursively
file { '/data/':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure => 'file',
  content => "location /hbnb_static {\n\talias /data/web_static/current/;\n}\n",
  notify => Service['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
