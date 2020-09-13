const path = require('path');

module.exports = {
  entry: ['./js/navbar.jsx', './js/table.jsx', './js/header.jsx'],
  output: {
    path: path.join(__dirname, '/static/'),
    filename: 'bundle.js',
  },
  module: {
    loaders: [
      {
        // Test for js or jsx files
        test: /\.jsx?$/,
        loader: 'babel-loader',
        query: {
          // Convert ES6 syntax to ES5 for browser compatibility
          presets: ['env', 'react'],
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};
