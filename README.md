Bookworm-Mallet
===============

Bookworm Mallet integration

This is a Bookworm extension.

This particular extensions supplements a Bookworm's "master_bookcounts" file with a `master_topicWords` file that otherwise resembles but that includes a `topic` column, created by MALLET. All the necessary work will happen on running `make` in the directory; some dependencies are not automatically installed.

Unlike a "good" bookworm extension, this one actually has a few bits of code in the API to support it. (Because that syntax for something other than `master_bookcounts` isn't transparently supported.) But I think it's worth it in this case, because it's make it possible to break apart a topic model at the unigram level.
