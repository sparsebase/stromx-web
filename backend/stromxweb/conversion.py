# -*- coding: utf-8 -*-

import base64
import cv2
import io
import numpy as np
import re

import stromx.runtime
import stromx.cvsupport

from error import Failed

def isNumber(variant):
    if variant.isVariant(stromx.runtime.Variant.INT):
        return True
    elif variant.isVariant(stromx.runtime.Variant.BOOL):
        return True
    elif variant.isVariant(stromx.runtime.Variant.TRIGGER):
        return True
    else:
        return False
    
def isString(variant):
    if variant.isVariant(stromx.runtime.Variant.STRING):
        return True
    else:
        return False
    
def hasStringRepresentation(variant):
    if variant.isVariant(stromx.runtime.Variant.STRING):
        return True
    elif variant.isVariant(stromx.runtime.Variant.MATRIX):
        return True
    elif variant.isVariant(stromx.runtime.Variant.IMAGE):
        return True
    else:
        return False
    
def toPythonObserverValue(variant, data):
    if variant.isVariant(stromx.runtime.Variant.IMAGE):
        return stromxImageToData(data)
    elif variant.isVariant(stromx.runtime.Variant.LIST):
        return stromxListToData(data)
    else:
        return toPythonValue(variant, data)
    
def toPythonValue(variant, data):
    if data.variant().isVariant(stromx.runtime.Variant.NONE):
        return None
    
    if variant.isVariant(stromx.runtime.Variant.INT):
        return int(data.get())
    elif variant.isVariant(stromx.runtime.Variant.FLOAT):
        return float(data.get())
    elif variant.isVariant(stromx.runtime.Variant.BOOL):
        return bool(data.get())
    elif variant.isVariant(stromx.runtime.Variant.STRING):
        return str(data.get())
    elif variant.isVariant(stromx.runtime.Variant.TRIGGER):
        return 0
    elif variant.isVariant(stromx.runtime.Variant.IMAGE):
        return {'width': data.width(), 'height': data.height() }
    elif variant.isVariant(stromx.runtime.Variant.MATRIX):
        return stromxMatrixToData(data)
    elif variant.isVariant(stromx.runtime.Variant.LIST):
        return {'numItems': len(data.content()) }
    else:
        return 0
       
def toStromxData(variant, value):
    if variant.isVariant(stromx.runtime.Variant.BOOL):
        return stromx.runtime.Bool(bool(value))
    elif variant.isVariant(stromx.runtime.Variant.ENUM):
        return stromx.runtime.Enum(value)
    elif variant.isVariant(stromx.runtime.Variant.UINT_8):
        return stromx.runtime.UInt8(value)
    elif variant.isVariant(stromx.runtime.Variant.UINT_16):
        return stromx.runtime.UInt16(value)
    elif variant.isVariant(stromx.runtime.Variant.UINT_32):
        return stromx.runtime.UInt32(value)
    elif variant.isVariant(stromx.runtime.Variant.INT_8):
        return stromx.runtime.Int8(value)
    elif variant.isVariant(stromx.runtime.Variant.INT_16):
        return stromx.runtime.Int16(value)
    elif variant.isVariant(stromx.runtime.Variant.INT_32):
        return stromx.runtime.Int32(value)
    elif variant.isVariant(stromx.runtime.Variant.FLOAT_32):
        return stromx.runtime.Float32(value)
    elif variant.isVariant(stromx.runtime.Variant.FLOAT_64):
        return stromx.runtime.Float64(value)
    elif variant.isVariant(stromx.runtime.Variant.STRING):
        return stromx.runtime.String(str(value))
    elif variant.isVariant(stromx.runtime.Variant.TRIGGER):
        return stromx.runtime.TriggerData()
    elif variant.isVariant(stromx.runtime.Variant.IMAGE):
        return dataToStromxImage(value)
    elif variant.isVariant(stromx.runtime.Variant.INT_32_MATRIX):
        return dataToStromxMatrix(value, stromx.runtime.Matrix.ValueType.INT_32)
    elif variant.isVariant(stromx.runtime.Variant.FLOAT_32_MATRIX):
        return dataToStromxMatrix(value, stromx.runtime.Matrix.ValueType.FLOAT_32)
    elif variant.isVariant(stromx.runtime.Variant.MATRIX):
        return dataToStromxMatrix(value, stromx.runtime.Matrix.ValueType.FLOAT_32)
    else:
        return None
    
def variantToString(variant):
    if variant.isVariant(stromx.runtime.Variant.FLOAT):
        return 'float'
    elif variant.isVariant(stromx.runtime.Variant.TRIGGER):
        return 'trigger'
    elif variant.isVariant(stromx.runtime.Variant.ENUM):
        return 'enum'
    elif variant.isVariant(stromx.runtime.Variant.INT):
        return 'int'
    elif variant.isVariant(stromx.runtime.Variant.BOOL):
        return 'bool'
    elif variant.isVariant(stromx.runtime.Variant.STRING):
        return 'string'
    elif variant.isVariant(stromx.runtime.Variant.IMAGE):
        return 'image'
    elif variant.isVariant(stromx.runtime.Variant.MATRIX):
        return 'matrix'
    elif variant.isVariant(stromx.runtime.Variant.LIST):
        return 'list'
    else:
        return 'none'
    
def stromxImageToData(stromxData):
    # make sure this is an image
    image = stromx.runtime.Image.data_cast(stromxData)
    if not image:
        raise Failed()
        
    array = np.asarray(image.data())
    rows = image.rows()
    cols = image.cols()
    
    # expand the color channel into the row
    if not image.variant().isVariant(stromx.runtime.Variant.MONO_IMAGE):
        array = array.reshape((rows, cols / 3, 3))
    
    # convert to BGR if necessary
    if image.pixelType() == stromx.runtime.Image.PixelType.RGB_24:
        cv2.cvtColor(array, cv2.COLOR_RGB2BGR, array)
    
    _, jpg = cv2.imencode('.jpg', array)
    values = 'data:image/jpg;base64,{0}'.format(
                                base64.encodestring(jpg.data).replace("\n", ""))
    data = {
        'width': image.width(),
        'height': image.height(),
        'values': values
    }
    
    return data

def stromxMatrixToData(stromxData):
    # make sure this is a matrix
    matrix = stromx.runtime.Matrix.data_cast(stromxData)
    if not matrix:
        raise Failed()
        
    array = np.asarray(matrix.data())
    
    data = {
        'rows': matrix.rows(),
        'cols': matrix.cols(),
        'values': array.tolist()
    }
    
    return data

def stromxListToData(stromxList):
    values = []
    for item in stromxList.content():
        value = {
            'variant': {
                'ident': variantToString(item.variant())
            },
            'value': toPythonObserverValue(item.variant(), item)
        }
        values.append(value)
    
    return { 'numItems': len(values), 'values': values }

def dataToStromxImage(data):
    content = re.sub("data:.*;base64,", "", data['values'], re.MULTILINE)
    buf = np.frombuffer(base64.decodestring(content), dtype = np.uint8)
    array = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
    
    if len(array.shape) == 3 and array.shape[2] == 3:
        image = stromx.cvsupport.Image(array.shape[1], array.shape[0],
                                       stromx.runtime.Image.PixelType.BGR_24)
        imageData = np.asarray(image.data())
        imageData[:, :] = array.reshape(array.shape[0], array.shape[1] * 3)
    elif len(array.shape) == 2:
        image = stromx.cvsupport.Image(array.shape[1], array.shape[0],
                                       stromx.runtime.Image.PixelType.MONO_8)
        imageData = np.asarray(image.data())
        imageData[:, :] = array.reshape(array.shape[0], array.shape[1])
    else:
        assert(False)
    return image
    
def dataToStromxMatrix(data, valueType):
    matrix = stromx.cvsupport.Matrix(data['rows'], data['cols'], valueType)
    matrixData = np.asarray(matrix.data());
    matrixData[:, :] = data['values']
    
    return matrix

def stromxColorToString(color):
    return '#{0:02x}{1:02x}{2:02x}'.format(color.r(), color.g(), color.b())

def stringToStromxColor(string):
    red = int(string[1:3], 16)
    green = int(string[3:5], 16)
    blue = int(string[5:], 16)
    return stromx.runtime.Color(red, green, blue)