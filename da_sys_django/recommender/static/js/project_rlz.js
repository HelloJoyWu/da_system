const PROJECT_VERSION={
  "frontend": "0.0.2",
  "jquery": "latest 3.2.1",
};

for (var [_module, _version] of Object.entries(PROJECT_VERSION)) {
  console.log(_module, ": ", _version);
};
