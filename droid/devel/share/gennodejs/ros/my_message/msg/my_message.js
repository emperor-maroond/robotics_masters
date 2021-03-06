// Auto-generated. Do not edit!

// (in-package my_message.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class my_message {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.some_floats = null;
    }
    else {
      if (initObj.hasOwnProperty('some_floats')) {
        this.some_floats = initObj.some_floats
      }
      else {
        this.some_floats = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type my_message
    // Serialize message field [some_floats]
    bufferOffset = _arraySerializer.float64(obj.some_floats, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type my_message
    let len;
    let data = new my_message(null);
    // Deserialize message field [some_floats]
    data.some_floats = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.some_floats.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'my_message/my_message';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '97ab95377be0b99d91d817753c93dd06';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] some_floats
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new my_message(null);
    if (msg.some_floats !== undefined) {
      resolved.some_floats = msg.some_floats;
    }
    else {
      resolved.some_floats = []
    }

    return resolved;
    }
};

module.exports = my_message;
