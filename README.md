## Amazon EC2 MSSQL Workshop

workshop for building mssql always on basic availability group on window and Linux. Build Amazon FSx for managed shared file service, AWS Directory services for Identity management and Amazon EC2 to create a Well-Architected Microsoft SQL solution.

## Building the Workshop site

The content of the workshops is built using [hugo](https://gohugo.io/). 

To build the content
 * clone this repository
 * [install hugo](https://gohugo.io/getting-started/installing/)
 * The project uses [hugo learn](https://github.com/matcornic/hugo-theme-learn/) template as a git submodule. To update the content, execute the following code
```bash
pushd themes/learn
git submodule init
git submodule update --checkout --recursive
popd
```
 * Run hugo to generate the site, and point your browser to http://localhost:1313
```bash
hugo serve -D
```

## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.
