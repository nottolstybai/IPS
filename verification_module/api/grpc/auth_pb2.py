# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nauth.proto\x12\x04\x61uth\x1a\x1bgoogle/protobuf/empty.proto\"H\n\x13RegistrationRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\";\n\x1aRegistrationWithKeyRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\"/\n\x0cLoginRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\"\n\rTokenResponse\x12\x11\n\tauthToken\x18\x01 \x01(\t\"\x1d\n\tMeMessage\x12\x10\n\x08username\x18\x01 \x01(\t2\xf8\x01\n\x04\x41uth\x12\x30\n\x05Login\x12\x12.auth.LoginRequest\x1a\x13.auth.TokenResponse\x12>\n\x0cRegistration\x12\x19.auth.RegistrationRequest\x1a\x13.auth.TokenResponse\x12O\n\x13RegistrationWithKey\x12 .auth.RegistrationWithKeyRequest\x1a\x16.google.protobuf.Empty\x12-\n\x02Me\x12\x16.google.protobuf.Empty\x1a\x0f.auth.MeMessageB\x19\xaa\x02\x16MVCS.Presentation.gRPCb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002\026MVCS.Presentation.gRPC'
  _globals['_REGISTRATIONREQUEST']._serialized_start=49
  _globals['_REGISTRATIONREQUEST']._serialized_end=121
  _globals['_REGISTRATIONWITHKEYREQUEST']._serialized_start=123
  _globals['_REGISTRATIONWITHKEYREQUEST']._serialized_end=182
  _globals['_LOGINREQUEST']._serialized_start=184
  _globals['_LOGINREQUEST']._serialized_end=231
  _globals['_TOKENRESPONSE']._serialized_start=233
  _globals['_TOKENRESPONSE']._serialized_end=267
  _globals['_MEMESSAGE']._serialized_start=269
  _globals['_MEMESSAGE']._serialized_end=298
  _globals['_AUTH']._serialized_start=301
  _globals['_AUTH']._serialized_end=549
# @@protoc_insertion_point(module_scope)