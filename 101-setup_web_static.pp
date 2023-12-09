# 101-setup_web_static.pp

# Ensure /data exists with the right permission
file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Install Nginx if not already installed
package { 'nginx':
  ensure => 'installed',
}

# Create necessary folders
file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure => 'file',
  content => '<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0644',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure => 'file',
  content => "location /hbnb_static {\n\talias /data/web_static/current/;\n}\n",
  owner  => 'root',
  group  => 'root',
  mode   => '0644',
  notify => Service['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure => 'running',
  enable => true,
}
