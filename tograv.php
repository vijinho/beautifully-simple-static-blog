<?php
// Covert markdown content pages to grav
// https://learn.getgrav.org/
// see https://learn.getgrav.org/cookbook/tutorials/create-a-blog

// get all markdown files
$files = array_merge(glob('content/*.md'), glob('content.private/*.md'));

// where to save converted markdown files for grav
$targetfolder = "grav/01.blog/";
$targetfile = 'item.md';

foreach ($files as $file) {
    $private = (false !== stristr($file, 'content.private/'));

    // read slug from filename
    $slug = substr(basename($file), 0, -3);

    // read in metadata header for file
    $lines = file($file);
    $hstart = $hend = false;
    foreach ($lines as $i => $line) {
        $line = trim($lines[$i]);
        $lines[$i] = $line;
        if ('---' == $line) {
            if (empty($hstart)) {
                unset($lines[$i]);
                $hstart = $i + 1;
            } elseif (empty($hend)) {
                unset($lines[$i]);
                $hend = $i - 1;
            }
        }
    }

    // do not process files with no metadata
    if (empty($hend)) {
        continue;
    }

    $headings = [];
    if (!empty($private)) {
        $headings['published'] = 'false';
    }
    for ($i = $hstart; $i <= $hend; $i++) {
        $metadata = preg_split("/:/", $lines[$i]);
        $key = trim($metadata[0]);
        $value = trim($metadata[1]);
        switch ($key) {
            case 'tags':
                $key = 'taxonomy';
                $value = "\n\tcategory: blog\n\ttag: $value\n\tauthor: vijay";
                break;
            case 'permalink':
                $key = 'slug';
                $value = substr(basename($value), 0, -5);
                break;
            case 'date':
                $value = strftime("%d-%m-%Y %R", strtotime(trim(substr($lines[$i], 6))));

        }
        $headings[$key] = $value;
        unset($lines[$i]);
    }

        // new folder for content
    $newfolder = $targetfolder . $slug;
    // create the new folder for content
    if (!file_exists($newfolder) && !mkdir($newfolder,0777,true)) {
        echo "FAILED creating folder: $newfolder\n";
        continue;
    }

    // write the markdown file into the content folder
    // build the new new markdown header text for grav
    $header = "---\n";
    foreach ($headings as $k => $v) {
        $header .= "$k: $v\n";
    }
    $header .= "---\n";
        // content text
    $content = str_replace('(/content/', '(../content/', join("\n", $lines));
    $filecontents = $header . $content;
    $newfile = $newfolder . '/' . $targetfile;
    if (!file_put_contents($newfile, $filecontents)) {
        echo "FAILED writing file: $newfile\n";
    }
}


$newfile = $targetfolder . '/blog.md';
$filecontents = "---\n
content:\n
    items: '@self.children'\n
---\n";
if (!file_put_contents($newfile, $filecontents)) {
    echo "FAILED writing blog index file: $newfile\n";
}
