{
  'targets':[
    {
      'target_name':'hello',
      'type':'executable',
      'sources':[
        'main.cpp',
      ],
      'include_dirs': [
        '../deps/',
      ],
      'dependencies': [
        '../deps/lib1/lib1.gyp:lib1',
      ],
    },
  ]
}
