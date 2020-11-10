suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]


def humansize(nbytes):
    # Sourced from stackoverflow - I forgot to grab the ref
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])
