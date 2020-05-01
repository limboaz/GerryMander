/*
The MIT License (MIT)

Copyright (c) 2013 Calvin Metcalf

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 */

'use strict';
import * as shp from 'shpjs';

/* global cw, shp */
L.Shapefile = L.GeoJSON.extend({
  options: {
    importUrl: 'shp.js'
  },

  initialize: function(file, options) {
    L.Util.setOptions(this, options);
    if (typeof cw !== 'undefined') {
      /*eslint-disable no-new-func*/
      if (!options.isArrayBuffer) {
        this.worker = cw(new Function('data', 'cb', 'importScripts("' + this.options.importUrl + '");shp(data).then(cb);'));
      } else {
        this.worker = cw(new Function('data', 'importScripts("' + this.options.importUrl + '"); return shp.parseZip(data);'));
      }
      /*eslint-enable no-new-func*/
    }
    L.GeoJSON.prototype.initialize.call(this, {
      features: []
    }, options);
    this.addFileData(file);
  },

  addFileData: function(file) {
    var self = this;
    this.fire('data:loading');
    if (typeof file !== 'string' && !('byteLength' in file)) {
      var data = this.addData(file);
      this.fire('data:loaded');
      return data;
    }
    if (!this.worker) {
      shp(file).then(function(data) {
        self.addData(data);
        self.fire('data:loaded');
      }).catch(function(err) {
        self.fire('data:error', err);
      })
      return this;
    }
    var promise;
    if (this.options.isArrayBufer) {
      promise = this.worker.data(file, [file]);
    } else {
      promise = this.worker.data(cw.makeUrl(file));
    }

    promise.then(function(data) {
      self.addData(data);
      self.fire('data:loaded');
      self.worker.close();
    }).then(function() {}, function(err) {
      self.fire('data:error', err);
    })
    return this;
  }
});

L.shapefile = function(a, b, c) {
  return new L.Shapefile(a, b, c);
};
