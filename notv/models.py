from django.db import models
from django.contrib import admin
from datetime import datetime
from django.contrib import admin

class Up(models.Model):
    name = models.CharField(max_length = 200)
    fromSite = models.CharField(max_length = 255, default = '')

    def getAllUnreadVideos(self):
        return Video.objects.filter(up = self, read = False)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length = 255, default = '')
    up = models.ForeignKey(Up)
    create = models.DateTimeField(auto_now_add = True)
    read = models.BooleanField(default = False)
    url = models.CharField(max_length = 255, default = '')
    pic = models.CharField(max_length = 255, default = '')

    def __str__(self):
        return self.title


class UpAdmin(admin.ModelAdmin):
    list_display = ('name', 'bilibilUrl', 'videoCount', 'unreadVideoCount')

    def videoCount(self, up):
        return Video.objects.filter(up = up).count()

    videoCount.short_description = 'Video Count'

    def unreadVideoCount(self, up):
        return up.getAllUnreadVideos().count()

    unreadVideoCount.short_description = 'Unread'

    def bilibilUrl(self, up):
        return '<a href="http://space.bilibili.com/%d/">%s</a>' % (up.id, up.name)

    bilibilUrl.short_description = 'URL'
    bilibilUrl.allow_tags = True


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'up', 'create', 'read')
    list_editable = ('read', )

    ordering = ['-create']



admin.site.register(Up, UpAdmin)
admin.site.register(Video, VideoAdmin)