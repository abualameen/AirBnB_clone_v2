# Puppet manifest for setting up web servers for web_static deployment

# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test/':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  content => "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>",
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create or recreate symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Update Nginx configuration
file_line { 'nginx_config':
  path    => '/etc/nginx/sites-available/default',
  line    => ' \ \n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}',
  match   => 'server_name _;',
  require => Package['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File_line['nginx_config'],
}
